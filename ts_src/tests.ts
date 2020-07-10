import { expect } from 'chai';
import { replace } from './replace';


describe('Symbols', () => {
  describe('replace alpha', () => {
    it('converts', done => {
      expect(replace('\\alpha')).to.equal('α');
      done();
    });
  });

  describe('combining mark', () => {
    it('adds dot to a', done => {
      expect(replace('\\dot{a}')).to.equal('ȧ');
      done();
    });
    it('adds dot to alpha', done => {
      expect(replace('\\dot{\\alpha}')).to.equal('α̇');
      done();
    });
    it('empty combining char', done => {
      expect(replace('\\breve{}')).to.equal('˘');
      done();
    });
    it('incomplete combining char', done => {
      expect(replace('\\breve{')).to.equal('\\breve{');
      done();
    });
  });
});
