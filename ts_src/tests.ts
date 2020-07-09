import { expect } from 'chai';
import { replace } from './replace';


describe('Symbols', () => {
  describe('alpha', () => {
    it('converts', done => {
      expect(replace('\\alpha')).to.equal('α');
      done();
    });
  });
});
