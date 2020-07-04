import { expect } from 'chai';
import { replace } from './replace';


describe('Symbols', () => {
  describe('alpha', () => {
    it('converts', done => {
      expect(replace(['\\alpha'])[0]).to.equal('α');
      done();
    });
  });
});
